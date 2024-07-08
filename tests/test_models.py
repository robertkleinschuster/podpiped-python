from podpiped.models import RelatedStream


def test_should_extract_video_id_from_related_stream():
    related_stream = RelatedStream(url='/watch?v=a05my9OegME')
    assert related_stream.video_id == 'a05my9OegME'

    related_stream = RelatedStream(url='')
    assert related_stream.video_id is None
