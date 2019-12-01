const PNG = require('pngjs').PNG;
const fs = require('fs');
const jsondata = JSON.parse(fs.readFileSync('tmp.json'));
const name = process.argv[2];
const u = jsondata.u;
const v = jsondata.v;

const width = jsondata.width
const height = jsondata.height - 1

const png = new PNG({
    colorType: 2,
    filterType: 4,
    width: width,
    height: height
});

for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
        const i = (y * width + x) * 4;
        const k = y * width + Math.floor(x) % width;
        if (u.values[k] < u.specs.minimum || u.values[k] > u.specs.maximum) {
            png.data[i + 0] = 0;
        }
        else {
            png.data[i + 0] = Math.floor(255 * (u.values[k] - u.specs.minimum) / (u.specs.maximum - u.specs.minimum));
            //console.log(u.specs.maximum);
            //console.log(Math.floor(255 * (u.values[k] - u.specs.minimum) / (u.specs.maximum - u.specs.minimum)));
        }
        if (v.values[k] < v.specs.minimum || v.values[k] > v.specs.maximum) {
            png.data[i + 1] = 0;
        }
        else {
            png.data[i + 1] = Math.floor(255 * (v.values[k] - v.specs.minimum) / (v.specs.maximum - v.specs.minimum));
        }
        png.data[i + 2] = 0;
        png.data[i + 3] = 255;
    }
}
console.log(name)
png.pack().pipe(fs.createWriteStream(name + '.png'));

fs.writeFileSync(name + '.json', JSON.stringify({
    source: 'http://nomads.ncep.noaa.gov',
    date: formatDate(u.dataDate + '', u.dataTime),
    width: width,
    height: height,
    uMin: u.specs.minimum,
    uMax: u.specs.maximum,
    vMin: v.specs.minimum,
    vMax: v.specs.maximum
}, null, 2) + '\n');

function formatDate(date, time) {
    return date.substr(0, 4) + '-' + date.substr(4, 2) + '-' + date.substr(6, 2) + 'T' +
        (time < 10 ? '0' + time : time) + ':00Z';
}