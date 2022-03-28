import Head from "next/head";
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
    <>
      <Head>
        <title>Notifications</title>
      </Head>
      <div className="p-5">
        {notifications.map((notification, index) => (
          <Alert
            key={index}
            severity={notification.severity}
            variant="filled"
            onClose={() => handleClose(index)}
            className="border-3 mb-4"
          >
            {notification.message}
          </Alert>
        ))}
      </div>
    </>
  );
}
