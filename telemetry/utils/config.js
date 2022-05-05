const toml = require("toml");
const fs = require("fs");

function config() {
  const configPath = `${process.cwd()}/config.toml`;
  const config = toml.parse(fs.readFileSync(configPath, "utf8"));
  return config;
}

module.exports = config();