import PropTypes from "prop-types";
import { useRouter } from "next/router";
import Link from "next/link";
import DashboardIcon from "@mui/icons-material/Dashboard";
import LinkIcon from "@mui/icons-material/Link";
import SettingsIcon from "@mui/icons-material/Settings";
import BarChartIcon from "@mui/icons-material/BarChart";
import BookIcon from "@mui/icons-material/Book";
import LanguageIcon from "@mui/icons-material/Language";
import DirectionsCarIcon from "@mui/icons-material/DirectionsCar";
import WidgetsIcon from "@mui/icons-material/Widgets";
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
import { useAtom } from "jotai";
import notificationsAtom from "../utils/notificationsAtom";

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
    text: "Notifications",
    icon: <NotificationsIcon />,
    href: "/notifications",
  },
  {
    text: "Metrics",
    icon: <BarChartIcon />,
    href: "/metrics",
  },
  {
    text: "Widget Studio",
    icon: <WidgetsIcon />,
    href: "/widget-studio",
  },
  {
    text: "Car Settings",
    icon: <DirectionsCarIcon />,
    href: "/car-settings",
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

  const getStyles = (href) => (router.pathname === href ? "bg-blue-200" : "");
  console.log(notifications);
  return (
    <div className="w-60 bg-white">
      <List>
        {primary_items.map((item, index) => (
          <Link
            key={index}
            href={item.href}
            style={{ textDecoration: "none", color: "black" }}
            onClick={(e) => handleClick(e, item.href)}
            passHref
          >
            <a>
              <ListItem
                button
                onClick={props.closeDrawer}
                className={getStyles(item.href)}
              >
                <ListItemIcon>
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
                <ListItemText primary={item.text} />
              </ListItem>
            </a>
          </Link>
        ))}
      </List>
      <Divider />
      <List>
        {secondary_items.map((item, index) => (
          <a
            key={index}
            target="_blank"
            rel="noreferrer"
            href={item.href}
            className="no-underline text-black"
          >
            <ListItem button onClick={props.closeDrawer}>
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
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
