import {
  Card,
  CardActions,
  CardContent,
  CardMedia,
  IconButton,
  Typography,
} from "@mui/material";
import { useParams } from "react-router-dom";
import { DefaultService, Movie, Session } from "../client";
import { useEffect, useState } from "react";
import { Check, Close } from "@mui/icons-material";

interface MovieCardProps {
  movie: Movie;
}
export function MovieCard({ movie }: MovieCardProps) {
  return (
    <Card sx={{ maxWidth: 345 }}>
      <CardMedia
        sx={{ height: 140 }}
        image={movie.image_url}
        title={movie.title}
      />
      <CardContent>
        <Typography gutterBottom variant="h5" component="div">
          {movie.title}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Movie description
        </Typography>
      </CardContent>
      <CardActions disableSpacing>
        <IconButton>
          <Check />
        </IconButton>
        <IconButton>
          <Close />
        </IconButton>
      </CardActions>
    </Card>
  );
}

export default function SessionDetails() {
  const { sessionId } = useParams<{ sessionId: string }>() as Record<
    string,
    string
  >;

  const [session, setSession] = useState<Session | null>(null);
  const [nextMovie, setNextMovie] = useState<Movie | null>(null);

  useEffect(() => {
    const fetchData = async (): Promise<void> => {
      setSession(
        await DefaultService.getSessionV1SessionSessionIdGet(sessionId),
      );
    };
    fetchData();
  }, [sessionId]);

  useEffect(() => {
    if (session === null) return;

    const fetchData = async (): Promise<void> => {
      setNextMovie(
        await DefaultService.getNextMovieV1SessionSessionIdNextMovieGet(
          session.id,
        ),
      );
    };
    fetchData();
  }, [session]);

  if (session === null || nextMovie === null) {
    return <Typography>Loading...</Typography>;
  }
  return <MovieCard movie={nextMovie} />;
}
