import React from "react";
import { Member } from "./Member.js";

export const Members = () => {
  const members = [
    {
      name: "Alexandre Girold",
      bio: "Future CEO of Google. I am studying at EPITA in order to acquire the necessary skills to achieve my goals. I am glad that I can work on Autopylot with such a great team! See you in 6 years. ",
      src: "/images/alexandre-girold.jpg",
      login: "alexandre.girold",
    },
    {
      name: "Maxime Ellerbach",
      bio: "Let's face it, I am kinda the BBB around here (Big Bad Boss). Yet I love the people i am working with, they are smart and devoted to the task. Also i am hella good at programming.",
      src: "/images/maxime-ellerbach.jpg",
      login: "maxime.ellerbach",
    },
    {
      name: "Maxime Gay",
      bio: "Fuck I am so hot, normal I am from the south of France. Yet dispite being a siddist I am actually smart and I love money.",
      src: "/images/maxime-gay.jpg",
      login: "maxime.gay",
    },
    {
      name: "Mickaël Bobovitch",
      bio: "Hot, sexy and russian. I am a full stack develloper with a heart of gold. I am glad to be in this wonderfull team of smart and nice developpers (Alex is kinda da best).",
      src: "/images/mickael-bobovitch.jpg",
      login: "mickael.bobovitch",
    },
  ];

  return (
    <div className="w-screen min-h-screen bg-white">
      <div className="pt-12 mx-auto flex-col">
        <div>
          <h1 className="h text-center">The Team</h1>
        </div>
        <div className="flex flex-wrap justify-center w-full mx-auto">
          {members.map((member) => (
            <Member
              key={member.name}
              name={member.name}
              src={member.src}
              bio={member.bio}
              login={member.login}
            />
          ))}
        </div>
      </div>
    </div>
  );
};
