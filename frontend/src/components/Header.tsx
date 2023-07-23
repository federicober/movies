import AppBar from "@mui/material/AppBar";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import LibraryMusic from "@mui/icons-material/LibraryMusic";

interface HeaderProps {
  onLogout: () => void;
}

export default function Header(props: HeaderProps) {
  return (
    <AppBar position="static" sx={{ margin: 0, padding: 2, paddingLeft: 6 }}>
      <Toolbar>
        <IconButton
          size="large"
          edge="start"
          color="inherit"
          sx={{ marginRight: 2 }}
          href={import.meta.env.BASE_URL}
        >
          <LibraryMusic />
        </IconButton>
        <Typography
          variant="h4"
          component="a"
          href={import.meta.env.BASE_URL}
          sx={{ flexGrow: 1, textDecoration: "none", color: "inherit" }}
        >
          Movies
        </Typography>
        <Button color="inherit" onClick={props.onLogout}>
          Logout
        </Button>
      </Toolbar>
    </AppBar>
  );
}
