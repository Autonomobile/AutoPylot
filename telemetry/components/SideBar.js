import { useRouter } from "next/router";
import { useAtom } from "jotai";
import { notificationsAtom } from "../utils/atoms";
import PropTypes from "prop-types";
import Link from "next/link";
import DashboardIcon from "@mui/icons-material/Dashboard";
import LinkIcon from "@mui/icons-material/Link";
import SettingsIcon from "@mui/icons-material/Settings";
import BarChartIcon from "@mui/icons-material/BarChart";
import BookIcon from "@mui/icons-material/Book";
import LanguageIcon from "@mui/icons-material/Language";
import DirectionsCarIcon from "@mui/icons-material/DirectionsCar";
import SettingsRemoteIcon from "@mui/icons-material/SettingsRemote";
import NotificationsIcon from "@mui/icons-material/Notifications";
import {
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Badge,
} from "@mui/material";

const primary_items = [
  {
    text: "Dashboard",
    icon: <DashboardIcon />,
    href: "/",
  },
  {
    text: "Remote Control",
    icon: <SettingsRemoteIcon />,
    href: "/remote-control",
  },
  {
    text: "Car Settings",
    icon: <DirectionsCarIcon />,
    href: "/car-settings",
  },
  {
    text: "Metrics",
    icon: <BarChartIcon />,
    href: "/metrics",
  },
  {
    text: "Notifications",
    icon: <NotificationsIcon />,
    href: "/notifications",
  },
  {
    text: "General Settings",
    icon: <SettingsIcon />,
    href: "/general-settings",
  },
];

const secondary_items = [
  {
    text: "Github",
    icon: <LinkIcon />,
    href: "https://github.com/autonomobile/autopylot",
  },
  {
    text: "Website",
    icon: <LanguageIcon />,
    href: "https://autonomobile.github.io",
  },
  {
    text: "Specifications",
    icon: <BookIcon />,
    href: "https://github.com/Autonomobile/AutoPylot/blob/main/ressources/first-presentation/project-report/project-report.pdf",
  },
];

export default function SideBar(props) {
  const router = useRouter();
  const [notifications] = useAtom(notificationsAtom);

  const handleClick = (e, href) => {
    e.preventDefault();
    router.push(href);
  };

  const styles = (href) => (router.pathname === href ? "primary blanc-casse" : "");

  return (
    <div className="w-60 h-full sidebar secondary">
      <List>
        {primary_items.map((item, index) => (
          <Link
            key={index}
            href={item.href}
            onClick={(e) => handleClick(e, item.href)}
            passHref
          >
            <a>
              <ListItem
                button
                onClick={props.closeDrawer}
                className={styles(item.href)}
                sx={{
                  ":hover": {
                    bgcolor: "#2f2f2f",
                  },
                }}
              >
                <ListItemIcon className="blanc-casse">
                  {item.text === "Notifications" ? (
                    <Badge
                      badgeContent={notifications.length}
                      color="error"
                      anchorOrigin={{
                        vertical: "top",
                        horizontal: "left",
                      }}
                      overlap="circular"
                      invisible={notifications.length === 0}
                    >
                      {item.icon}
                    </Badge>
                  ) : (
                    <>{item.icon}</>
                  )}
                </ListItemIcon>
                <ListItemText className="blanc-casse" primary={item.text} />
              </ListItem>
            </a>
          </Link>
        ))}
      </List>
      <Divider className="divider" />
      <List>
        {secondary_items.map((item, index) => (
          <a key={index} target="_blank" rel="noreferrer" href={item.href}>
            <ListItem
              button
              onClick={props.closeDrawer}
              sx={{
                ":hover": {
                  bgcolor: "#2f2f2f",
                },
              }}
            >
              <ListItemIcon className="blanc-casse">{item.icon}</ListItemIcon>
              <ListItemText className="blanc-casse" primary={item.text} />
            </ListItem>
          </a>
        ))}
      </List>
    </div>
  );
}

SideBar.propTypes = {
  closeDrawer: PropTypes.func,
};
