// start-next.js
const { spawn } = require("child_process");

const child = spawn("npm", ["run", "start"], { stdio: "inherit", shell: true, cwd: "C:\\infoRUN\\Client" });

child.on("close", (code) => {
  console.log(`Next.js exited with code ${code}`);
});