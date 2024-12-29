from flask import Blueprint, request, jsonify
from db.models import (
    get_transcript_by_video_id,
    insert_transcript,
    update_metadata,
    get_transcript_record_by_id
)
from services.youtube_service import fetch_youtube_transcript, get_video_metadata
from services.llm_service import generate_summary_with_custom_llm

transcript_blueprint = Blueprint("transcripts", __name__)

@transcript_blueprint.route("/transcript", methods=["POST"])
def handle_transcript():
    data = request.get_json()
    video_id = data.get('video_id')
    title = data.get('title', None)
    summarize = data.get('summarize', False)

    if not video_id:
        return jsonify({"error": "Missing 'video_id' in request body"}), 400

    existing_record = get_transcript_by_video_id(video_id)
    if existing_record:
        record_id = existing_record['id']
        db_transcript = existing_record['transcript'] or ""
        db_summary = existing_record['summary'] or ""
        db_published_date = existing_record.get('published_date')
        db_channel_name = existing_record.get('channel_name')

        # If published_date or channel_name missing, fetch and update
        if not db_published_date or not db_channel_name:
            new_published_date, new_channel_name = get_video_metadata(video_id)
            if new_published_date or new_channel_name:
                update_metadata(record_id, new_published_date, new_channel_name)
                db_published_date = new_published_date or db_published_date
                db_channel_name = new_channel_name or db_channel_name

        return jsonify({
            "message": "Transcript record found/updated",
            "id": record_id,
            "title": existing_record['title'],
            "transcript": db_transcript,
            "summary": db_summary,
            "published_date": db_published_date,
            "channel_name": db_channel_name
        }), 200
    else:
        # No existing record
        try:
            transcript_text = fetch_youtube_transcript(video_id)
        except RuntimeError as e:
            return jsonify({"error": str(e)}), 400

        summary_text = None
        if summarize:
            summary_text = generate_summary_with_custom_llm(transcript_text)

        published_date, channel_name = get_video_metadata(video_id)
        new_id = insert_transcript(
            video_id,
            title,
            transcript_text,
            summary_text,
            published_date,
            channel_name
        )

        return jsonify({"message": "Transcript saved", "id": new_id}), 200

@transcript_blueprint.route("/transcript/<int:record_id>", methods=["GET"])
def get_transcript_record(record_id):
    result = get_transcript_record_by_id(record_id)

    if not result:
        return jsonify({"error": "Record not found"}), 404

    return jsonify(result), 200
