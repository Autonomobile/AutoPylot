import LiveView from "../components/LiveView";

const remote_control = () => {
  return (
    <div className="w-full">
      <div className="h-5 w-full"></div>

      <div className="w-full px-5">
        <LiveView />
      </div>
    </div>
  );
};

export default remote_control;
