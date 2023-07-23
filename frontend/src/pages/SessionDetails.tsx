import { Typography } from "@mui/material";
import { useParams } from "react-router-dom";
import { DefaultService, Session } from "../client";
import { useEffect, useState } from "react";

export default function SessionDetails() {
  const { sessionId } = useParams<{ sessionId: string }>() as Record<
    string,
    string
  >;

  const [session, setSession] = useState<Session | null>(null);

  useEffect(() => {
    const fetchData = async (): Promise<void> => {
      setSession(
        await DefaultService.getSessionV1SessionSessionIdGet(sessionId),
      );
    };
    fetchData();
  }, [sessionId]);

  if (session === null) {
    return <Typography>Loading...</Typography>;
  }
  return <Typography>In session</Typography>;
}
