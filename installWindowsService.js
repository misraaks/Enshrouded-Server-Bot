const Service = require('node-windows').Service;
const svc = new Service({
    name: 'Enshrouded Server Bot',
    description: 'Discord bot that starts and stops the Enshrouded server',
    script: 'C:\\Enshrouded-Server-Bot\\bot.js'
  });
  svc.on('install', () => {
    svc.start();
  });
  svc.install();