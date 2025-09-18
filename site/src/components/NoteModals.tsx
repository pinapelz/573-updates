import Popup from "reactjs-popup";
import React from "react";

export const EamuseMaintenancePopup: React.FC<{ isMoe: boolean }> = ({
  isMoe,
}) => {
  return (
    <Popup
      trigger={
        <button
          className={`mt-4 rounded px-2 py-1 ${isMoe ? "bg-pink-300 text-pink-900 hover:bg-pink-400" : "bg-gray-500 text-white hover:bg-gray-400"}`}
        >
          e-amusement Maintenance
        </button>
      }
      position="center center"
      modal
      closeOnDocumentClick
      overlayStyle={{
        backgroundColor: "rgba(0, 0, 0, 0.5)",
      }}
    >
      <div
        className={`p-6 rounded-lg shadow-lg ${isMoe ? "bg-pink-100 text-pink-900" : "bg-gray-900 text-white"} max-w-md mx-auto`}
      >
        <div className="flex justify-between items-center mb-3">
          <h3 className="text-lg">e-amusement Maintenance Information</h3>
        </div>
        <div className="mb-4">
          <p className="font-bold">Regular Daily Maintenance</p>
          <p className="mt-1 font-semibold">
            Every day from 5:00 AM to 7:00 AM (JST)
          </p>
          <p className="mt-1 text-right">
            In your local time:{" "}
            {(() => {
              const jst5am = new Date();
              jst5am.setUTCHours(20, 0, 0, 0); // 5AM JST is 8PM UTC the day before
              const jst7am = new Date();
              jst7am.setUTCHours(22, 0, 0, 0); // 7AM JST is 10PM UTC the day before
              const options: Intl.DateTimeFormatOptions = {
                hour: "2-digit",
                minute: "2-digit",
                hour12: true,
              };
              return `${jst5am.toLocaleTimeString([], options)} to ${jst7am.toLocaleTimeString([], options)}`;
            })()}
          </p>
          <p>
            e-amusement website, at-home Konasute games offline, Japan + Asia
            cabinets offline. USA cabinets exempt
          </p>
          <p className="font-bold mt-4">Monthly Extended Maintenance</p>
          <p className="mt-1 font-semibold">
            Every Third Tuesday from 2:00 AM to 7:00 AM (JST)
          </p>
          <p className="mt-1 text-right">
            In your local time:{" "}
            {(() => {
              const jst2am = new Date();
              jst2am.setUTCHours(17, 0, 0, 0);
              const jst7am = new Date();
              jst7am.setUTCHours(22, 0, 0, 0);
              const options: Intl.DateTimeFormatOptions = {
                hour: "2-digit",
                minute: "2-digit",
                hour12: true,
              };
              return `${jst2am.toLocaleTimeString([], options)} to ${jst7am.toLocaleTimeString([], options)}`;
            })()}
          </p>
          <p>
            ALL Cabinets + e-amusement services offline. This is moved 1 day
            earlier if that day is a Japanese Holiday.
          </p>
        </div>
        <div className="flex justify-end"></div>
      </div>
    </Popup>
  );
};

export const NesicaMaintenancePopup: React.FC<{ isMoe: boolean }> = ({
  isMoe,
}) => {
  return (
    <Popup
      trigger={
        <button
          className={`mt-4 rounded px-2 py-1 ${isMoe ? "bg-pink-300 text-pink-900 hover:bg-pink-400" : "bg-gray-500 text-white hover:bg-gray-400"}`}
        >
          NESiCA Maintenance
        </button>
      }
      position="center center"
      modal
      closeOnDocumentClick
      overlayStyle={{
        backgroundColor: "rgba(0, 0, 0, 0.5)",
      }}
    >
      <div
        className={`p-6 rounded-lg shadow-lg ${isMoe ? "bg-pink-100 text-pink-900" : "bg-gray-900 text-white"} max-w-md mx-auto`}
      >
        <div className="flex justify-between items-center mb-3">
          <h3 className="text-lg">NESiCA Maintenance Information</h3>
        </div>
        <div className="mb-4">
          <p className="font-bold">Regular Daily Maintenance</p>
          <p className="mt-1 font-semibold">
            Every day from 6:00 AM to 8:00 AM (JST)
          </p>
          <p className="mt-1 text-right">
            In your local time:{" "}
            {(() => {
              const jst5am = new Date();
              jst5am.setUTCHours(21, 0, 0, 0); // 6AM JST is 9PM UTC the day before
              const jst7am = new Date();
              jst7am.setUTCHours(23, 0, 0, 0); // 8AM JST is 11PM UTC the day before
              const options: Intl.DateTimeFormatOptions = {
                hour: "2-digit",
                minute: "2-digit",
                hour12: true,
              };
              return `${jst5am.toLocaleTimeString([], options)} to ${jst7am.toLocaleTimeString([], options)}`;
            })()}
          </p>
          <p>
            IC Cards are not accepted 15 minutes prior to start of maintenance
          </p>
        </div>
        <div className="flex justify-end"></div>
      </div>
    </Popup>
  );
};

export const AimeIntlMaintenanceInfo: React.FC<{ isMoe: boolean }> = ({
  isMoe,
}) => {
  return (
    <Popup
      trigger={
        <button
          className={`mt-4 rounded px-2 py-1 ${isMoe ? "bg-pink-300 text-pink-900 hover:bg-pink-400" : "bg-gray-500 text-white hover:bg-gray-400"}`}
        >
          Aime Maintenance
        </button>
      }
      position="center center"
      modal
      closeOnDocumentClick
      overlayStyle={{
        backgroundColor: "rgba(0, 0, 0, 0.5)",
      }}
    >
      <div
        className={`p-6 rounded-lg shadow-lg ${isMoe ? "bg-pink-100 text-pink-900" : "bg-gray-900 text-white"} max-w-md mx-auto`}
      >
        <div className="flex justify-between items-center mb-3">
          <h3 className="text-lg">Aime Maintenance Information</h3>
        </div>
        <div className="mb-4">
          <p className="font-bold">Regular Daily Maintenance</p>
          <p className="mt-1 font-semibold">
            Every day from 11:00 AM to 2:00 PM (PST)
          </p>
          <p className="mt-1 text-right">
            In your local time:{" "}
            {(() => {
              const pst11am = new Date();
              pst11am.setUTCHours(19, 0, 0, 0); // 11AM PST is 7PM UTC
              const pst2pm = new Date();
              pst2pm.setUTCHours(22, 0, 0, 0); // 2PM PST is 10PM UTC
              const options: Intl.DateTimeFormatOptions = {
                hour: "2-digit",
                minute: "2-digit",
                hour12: true,
              };
              return `${pst11am.toLocaleTimeString([], options)} to ${pst2pm.toLocaleTimeString([], options)}`;
            })()}
          </p>
          <p>
            Cabinets will operate only in GUEST MODE play mode during
            maintenance
          </p>
        </div>
        <div className="flex justify-end"></div>
      </div>
    </Popup>
  );
};

export const AllnetPrivateServerWarning: React.FC<{ isMoe: boolean }> = ({
  isMoe,
}) => {
  return (
    <Popup
      trigger={
        <button
          className={`mt-4 rounded px-2 py-1 ${isMoe ? "bg-pink-300 text-pink-900 hover:bg-pink-400" : "bg-gray-500 text-white hover:bg-gray-400"}`}
        >
          Private Networks
        </button>
      }
      position="center center"
      modal
      closeOnDocumentClick
      overlayStyle={{
        backgroundColor: "rgba(0, 0, 0, 0.5)",
      }}
    >
      <div
        className={`p-6 rounded-lg shadow-lg ${isMoe ? "bg-pink-100 text-pink-900" : "bg-gray-900 text-white"} max-w-md mx-auto`}
      >
        <div className="flex justify-between items-center mb-3">
          <h3 className="text-lg">Private Servers</h3>
        </div>
        <div className="mb-4">
          <p className="mt-1 mb-2">
            This game has prominent private networks in locations where official
            service was/is not available.
            <br /> <br /> Playdata on these private networks not shared nor
            transferrable with official service. Please take care to know the
            difference.
            <br /> <br />
            All information on this side refers to cabinets on the official
            network.
          </p>
        </div>
        <div className="flex justify-end"></div>
      </div>
    </Popup>
  );
};
