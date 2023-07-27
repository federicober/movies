import {
  Card,
  CardActions,
  CardContent,
  CardMedia,
  IconButton,
  Typography,
} from "@mui/material";
import { useParams } from "react-router-dom";
import {
  DefaultService,
  Movie,
  Session,
  SessionMatches,
  Vote,
} from "../client";
import { useCallback, useEffect, useState } from "react";
import { Check, Close } from "@mui/icons-material";
import SessionHeader from "./SessionHeader";

interface MovieCardProps {
  movie: Movie;
  onVote: (vote: Vote.vote) => void;
}
export function MovieCard({ movie, onVote }: MovieCardProps) {
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
      <CardActions>
        <IconButton onClick={() => onVote(Vote.vote.YES)}>
          <Check />
        </IconButton>
        <IconButton onClick={() => onVote(Vote.vote.NO)}>
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
  const [matches, setMatches] = useState<SessionMatches | undefined>(undefined);

  const refreshPage = useCallback(() => {
    if (session === null) return;
    const fetchData = async (): Promise<void> => {
      const [nextMovie, matches] = await Promise.all([
        DefaultService.getNextMovieV1SessionSessionIdNextMovieGet(session.id),
        DefaultService.getSessionMatchesV1SessionSessionIdMatchesGet(
          session.id,
        ),
      ]);
      setNextMovie(nextMovie);
      setMatches(matches);
    };
    fetchData();
  }, [session]);

  useEffect(() => {
    const fetchData = async (): Promise<void> => {
      setSession(
        await DefaultService.getSessionV1SessionSessionIdGet(sessionId),
      );
    };
    fetchData();
  }, [sessionId]);

  useEffect(() => {
    refreshPage();
  }, [refreshPage, session]);

  if (session === null || nextMovie === null) {
    return <Typography>Loading...</Typography>;
  }

  const onVote = async (vote: Vote.vote) => {
    DefaultService.voteForMovieV1SessionSessionIdMovieMovieIdPost(session.id, {
      movie_id: nextMovie.id,
      vote: vote,
    });
    refreshPage();
  };

  return (
    <>
      <SessionHeader session={session} matches={matches} />
      <MovieCard movie={nextMovie} onVote={onVote} />
    </>
  );
}
