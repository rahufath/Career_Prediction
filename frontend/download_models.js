/* eslint-disable */
const fs = require('fs');
const https = require('https');
const path = require('path');


const modelsDir = path.join(__dirname, 'public', 'models');
const baseUrl = 'https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights';

const files = [
    'tiny_face_detector_model-weights_manifest.json',
    'tiny_face_detector_model-shard1',
    'face_expression_model-weights_manifest.json',
    'face_expression_model-shard1',
    'face_landmark_68_model-weights_manifest.json',
    'face_landmark_68_model-shard1'
];

async function downloadFile(filename) {
    const filePath = path.join(modelsDir, filename);
    const file = fs.createWriteStream(filePath);

    return new Promise((resolve, reject) => {
        https.get(`${baseUrl}/${filename}`, (response) => {
            response.pipe(file);
            file.on('finish', () => {
                file.close();
                console.log(`Downloaded ${filename}`);
                resolve();
            });
        }).on('error', (err) => {
            fs.unlink(filePath, () => { }); // Delete the file async. (But we don't check the result)
            reject(err.message);
        });
    });
}

async function main() {
    if (!fs.existsSync(modelsDir)) {
        fs.mkdirSync(modelsDir, { recursive: true });
    }

    console.log('Downloading face-api models...');

    for (const file of files) {
        try {
            await downloadFile(file);
        } catch (e) {
            console.error(`Error downloading ${file}: ${e}`);
        }
    }

    console.log('All models downloaded!');
}

main();
