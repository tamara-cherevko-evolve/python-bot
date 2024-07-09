import { RocketIcon } from "lucide-react";

function DisconnectedMessage() {
  return (
    <div className="flex flex-col items-center justify-center mt-5">
      <RocketIcon className="w-12 h-12 text-gray-400" />
      <p className="text-lg font-bold text-gray-400">Disconnected</p>
    </div>
  );
}

export default DisconnectedMessage;
