import { Member } from "./Member.js";
import { members } from "../data/data.js";

export const Members = () => {

  return (
    <div className="w-screen min-h-screen bg-white">
      <div className="pt-12 mx-auto flex-col">
        <div>
          <h1 className="h text-center">The Team</h1>
        </div>
        <div className="flex flex-wrap justify-center w-full mx-auto">
          {members.map((member) => (
            <Member
              key={member.login}
              name={member.name}
              src={member.src}
              bio={member.bio}
              login={member.login}
            />
          ))}
        </div>
        {/* <p className="text-center mt-6">TODO ADD TEXT</p> */}
      </div>
    </div>
  );
};
