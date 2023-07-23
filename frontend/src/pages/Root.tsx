import {
  Avatar,
  AvatarGroup,
  List,
  ListItem,
  Stack,
  Tooltip,
  Typography,
} from "@mui/material";
import { DefaultService, Session } from "../client";
import { ReactNode, useEffect, useState } from "react";
import { Link } from "react-router-dom";

interface SessionAvatarProps {
  session: Session;
}

export function SessionAvatar({ session }: SessionAvatarProps): ReactNode {
  const title = `Session with ${session.members
    .map((user) => user.name)
    .join(", ")}`;
  return (
    <Tooltip title={title}>
      <Link
        to={`session/${session.id}`}
        style={{ textDecoration: "none", color: "inherit" }}
      >
        <Stack direction="row" alignItems="center" spacing={4}>
          <AvatarGroup max={4}>
            {session.members.map((user) => (
              <Avatar alt={user.name}>{user.name[0]}</Avatar>
            ))}
          </AvatarGroup>
          <Typography>{title}</Typography>
        </Stack>
      </Link>
    </Tooltip>
  );
}

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
          <SessionAvatar session={session} />
        </ListItem>
      ))}
    </List>
  );
}

export default function Root() {
  return <SessionsList />;
}
