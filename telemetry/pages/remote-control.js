import LiveView from "../components/LiveView";

export default function RemoteControl() {
  return (
    <div className="w-full">
      <div className="h-5 w-full"></div>

      <div className="w-full px-5">
        <LiveView />
      </div>
    </div>
  );
}
