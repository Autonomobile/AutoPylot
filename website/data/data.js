const members = [
  {
    name: "Alexandre Girold",
    bio: "Alexandre Girold is our marketing specialist and one of our developer on the software part of this project. A Member full of resources and ideas",
    src: "images/alexandre-girold.jpg",
    login: "alexandre.girold",
  },
  {
    name: "Maxime Ellerbach",
    bio: "Maxime Elerbach is our Team leader. Over 3 years of experience in autonomous cars and races. An enthusiastic leader for driving change to always reach our high targets.",
    src: "images/maxime-ellerbach.jpg",
    login: "maxime.ellerbach",
  },
  {
    name: "Maxime Gay",
    bio: "Maxime Gay is one of our developer on the software part of this project. Over many years of teamwork and pitching products.",
    src: "images/maxime-gay.jpg",
    login: "maxime.gay",
  },
  {
    name: "Mickaël Bobovitch",
    bio: "Mickael Bobovitch is our web developer. Over 4 years of experience in web development and 1 year as entrepreneur in Email Marketing and Affiliation. CTO of GenWork.fr",
    src: "images/mickael-bobovitch.jpg",
    login: "mickael.bobovitch",
  },
];

const items = [
  {
    title: "17/01",
    cardTitle: "Starting Project",
    cardDetailedText: "Brainstorming the project. Creating the roadmap. Planning the project. Creating the team, the logo and the brand. Github and Slack are ready. Our goals are to create a new autonomous car. ",
    media: {
      type: "IMAGE",
      source: {
        url: "/logo.svg",
      },
    },
  },
  {
    title: "29/01",
    cardTitle: "1st Race",
    cardDetailedText: "We can drive and control the car with our handmade Xbox Controller. Everything is built from scratch. We used a \"modular\" approach. The code is extensible and offer the possibility of easy scalling and maintenance.",
    media: {
      type: "IMAGE",
      source: {
        url: "/images/xbox.jpeg",
      },
    },
  },
  {
    title: "26/02",
    cardTitle: "2nd Race",
    cardDetailedText: "We are able to collect data from the car. We plan to create a web app to visualize metrics. We are looking to run a server with ElasticSearch, as we use JSON for our data. We created a simple and robust API to enable to communication",
    media: {
      type: "IMAGE",
      source: {
        url: "/images/data.jpeg",
      },
    },
  },
  {
    title: "19/03",
    cardTitle: "3rd Race",
    cardDetailedText: "Implementation of the telemetry Website. We used Next.js as it is fast and reliable. The coolest feature is a live view from the car's camera. Furthermore we have live metrics. We use Docker to run the server.",
    media: {
      type: "IMAGE",
      source: {
        url: "/images/ui.jpeg",
      },
    },
  },
  {
    title: "16/04",
    cardTitle: "4th Race",
    cardDetailedText: "We ameliorated the data processing. We used Tensorflow to build a basic convolutional neural network. The car is able to drive by itself. The training is done with multiple input source like real world data and simulated data.",
    media: {
      type: "IMAGE",
      source: {
        url: "/images/ai.jpg",
      },
    },
  },
  {
    title: "14/05",
    cardTitle: "5th Race",
    cardDetailedText: "Our car is now fully functional! The AI is well trained. Metrics collection is working well. The project approaches it's final state. We improved all the components and made great optimisatiion. Now our goal is to make out car unbeatable in races.",
    media: {
      type: "IMAGE",
      source: {
        url: "/images/car.jpeg",
      },
    },
  },
  {
    title: "04/06",
    cardTitle: "Last Race",
    cardDetailedText: "This is it! The final race. All the code is polished to perfection. The documentation is totally complete. The project is finished. All we have to do now is to win every races!",
    media: {
      type: "IMAGE",
      source: {
        url: "/images/end.png",
      },
    },
  },
];

exports = module.exports = { members, items };