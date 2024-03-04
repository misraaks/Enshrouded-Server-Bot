const Service = require('node-windows').Service;
const svc = new Service({
    name: 'Enshrouded Server Bot',
    description: 'Discord bot that starts and stops the Enshrouded server',
    script: 'C:\\Enshrouded-Server-Bot\\bot.js'
  });
  svc.on('uninstall',function(){
    console.log('Uninstall complete.');
    console.log('The service exists: ',svc.exists);
  });
  
  // Uninstall the service.
  svc.uninstall();