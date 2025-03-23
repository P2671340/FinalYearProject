const si = require('systeminformation'); // Import systeminformation module
const fs = require('fs'); // File system module to write output.json

async function runScan() {
  try {
    // Fetch system information
    const cpu = await si.cpu();
    const memory = await si.mem();
    const disk = await si.diskLayout();
    const network = await si.networkStats();

    // Prepare the output data
    const scanResults = {
      cpu: {
        manufacturer: cpu.manufacturer,
        brand: cpu.brand,
        cores: cpu.cores,
        speed: cpu.speed,
        times: cpu.times,
      },
      memory: {
        total: memory.total,
        free: memory.free,
        used: memory.used,
      },
      disk: disk.map(disk => ({
        type: disk.type,
        size: disk.size,
        mount: disk.mount,
      })),
      network: network.map(net => ({
        iface: net.iface,
        received_bytes: net.rx_bytes,
        transmitted_bytes: net.tx_bytes,
      })),
    };

    // Write the scan results to output.json
    fs.writeFileSync('output.json', JSON.stringify(scanResults, null, 2));

    console.log('Scan completed successfully!');
  } catch (error) {
    console.error('Error during system scan:', error);
    process.exit(1); // Exit with an error code
  }
}

// Run the scan
runScan();
