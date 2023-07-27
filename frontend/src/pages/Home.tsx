import { List, ListItem } from "@mui/material";
import { DefaultService, Session } from "../client";
import { ReactNode, useEffect, useState } from "react";
import SessionHeader from "./SessionHeader";

export function SessionsList(): ReactNode {
  const [sessions, setSessions] = useState<Session[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      setSessions(await DefaultService.listSessionsV1SessionGet());
    };
    fetchData();
  }, []);

  return (
    <List>
      {sessions.map((session) => (
        <ListItem key={session.id}>
          <SessionHeader session={session} />
        </ListItem>
      ))}
    </List>
  );
}

export default function Root() {
  return <SessionsList />;
}
