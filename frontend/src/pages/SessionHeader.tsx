import { Avatar, AvatarGroup, Stack, Tooltip, Typography } from "@mui/material";
import { Session, SessionMatches } from "../client";
import { ReactNode } from "react";
import { Link } from "react-router-dom";

interface SessionHeaderProps {
  session: Session;
  matches?: SessionMatches;
}

export default function SessionHeader({
  session,
  matches,
}: SessionHeaderProps): ReactNode {
  const title = `Session with ${session.members
    .map((user) => user.name)
    .join(", ")}`;
  return (
    <Tooltip title={title}>
      <Link
        to={`/session/${session.id}`}
        style={{ textDecoration: "none", color: "inherit" }}
      >
        <Stack direction="row" alignItems="center" spacing={4}>
          <AvatarGroup max={4}>
            {session.members.map((user) => (
              <Avatar alt={user.name}>{user.name[0]}</Avatar>
            ))}
          </AvatarGroup>
          <Typography>{title}</Typography>
          {matches !== undefined && (
            <Typography>{matches.count} matches</Typography>
          )}
        </Stack>
      </Link>
    </Tooltip>
  );
}
