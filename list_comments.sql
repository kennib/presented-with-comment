SELECT video.channel AS channel, video.title AS video,
  comment.site AS site, comment.author AS author, comment.url AS url,
  comment.comment AS comment
  FROM comment
    JOIN video ON comment.video = video.id
  WHERE DATE(video.date) > DATE('now', '-7 days')
  ORDER BY down_votes+up_votes DESC;
