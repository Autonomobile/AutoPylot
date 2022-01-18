import React from "react";
import { Member } from "./Member.js";

export const Members = () => {
  const members = [
    {
      name: "Maxime Ellerbach",
      bio: "Maxime Ellerbach is a member of the AutoPylot team.",
      src: "/images/maxime-ellerbach.jpg",
    },
    {
      name: "Maxime Gay",
      bio: "Maxime Gay is a member of the AutoPylot team.",
      src: "/images/maxime-gay.jpg",
    },
    {
      name: "Alexandre Girold",
      bio: "Alexandre Girold is a member of the AutoPylot team.",
      src: "/images/alexandre-girold.jpg",
    },
    {
      name: "Mickaël Bobovitch",
      bio: "Mickaël Bobovitch is a member of the AutoPylot team.",
      src: "/images/mickael-bobovitch.jpg",
    },
  ];

  return (
    <div className="w-screen min-h-screen bg-white">
      <div className="pt-12 mx-auto flex-col">
        <div>
          <h1 className="h text-center">The Team</h1>
        </div>
        <div className="flex flex-wrap lg:w-2/3 mx-auto">
          {members.map((member) => (
            <Member
              key={member.name}
              name={member.name}
              src={member.src}
              bio={member.bio}
            />
          ))}
        </div>
      </div>
    </div>
  );
};