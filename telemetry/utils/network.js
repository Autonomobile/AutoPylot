const os = require("os");

module.exports = {
  getLocalIpAdress: function getLocalIpAdress() {
    const interfaces = os.networkInterfaces();
    const addresses = [];
    for (const i in interfaces) {
      for (const j in interfaces[i]) {
        const address = interfaces[i][j];
        if (address.family === "IPv4" && !address.internal) {
          addresses.push(address.address);
        }
      }
    }
    if (addresses.length === 0) {
      return "";
    }
    return addresses;
  },
};