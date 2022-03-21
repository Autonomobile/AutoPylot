import { useAtom } from "jotai";
import { notificationsAtom } from "../utils/atoms";
import Alert from "@mui/material/Alert";

export default function Notifications() {
  const [notifications, setNotifications] = useAtom(notificationsAtom);

  function handleClose(index) {
    notifications.splice(index, 1);
    setNotifications([...notifications]);
  }

  return (
    <div className="p-5">
      {notifications.map((notification, index) => (
        <Alert
          key={index}
          severity={notification.severity}
          onClose={() => handleClose(index)}
          className="border-3 mb-4 primary text"
        >
          {notification.message}
        </Alert>
      ))}
    </div>
  );
}
