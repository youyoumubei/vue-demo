const CHUNK_SIZE = 2 * 1024 * 1024; // 2MB per chunk

const uploadFileInChunks = (file) => {
  const totalChunks = Math.ceil(file.size / CHUNK_SIZE);
  const uploadPromises = [];

  for (let i = 0; i < totalChunks; i++) {
    const start = i * CHUNK_SIZE;
    const end = Math.min(file.size, start + CHUNK_SIZE);
    const chunk = file.slice(start, end);

    uploadPromises.push(uploadChunk(chunk, i, totalChunks));
  }

  return Promise.all(uploadPromises);
};

const uploadChunk = (chunk, index, totalChunks) => {
  // Simulate an upload request
  return new Promise((resolve) => {
    console.log(`Uploading chunk ${index + 1}/${totalChunks}`);
    setTimeout(() => {
      resolve(`Chunk ${index + 1}/${totalChunks} uploaded`);
    }, 1000);
  });
};

const handleFileUpload = (file) => {
  uploadFileInChunks(file).then((results) => {
    console.log('All chunks uploaded:', results);
  }).catch((error) => {
    console.error('Error uploading chunks:', error);
  });
};

const readFileAsync = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
    reader.readAsArrayBuffer(file);
  });
};

const handleFileRead = async (file) => {
  try {
    const data = await readFileAsync(file);
    // Process data
    console.log('File read successfully:', data);
  } catch (error) {
    console.error('Error reading file:', error);
  }
};

<template>
  <div>
    <a-upload :before-upload="beforeUpload" :show-upload-list="false">
      <a-button icon="upload">Click to Upload</a-button>
    </a-upload>
    <div v-if="headers.length">
      <h3>Table Headers:</h3>
      <ul>
        <li v-for="(header, index) in headers" :key="index">{{ header }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import * as XLSX from 'xlsx';

export default {
  data() {
    return {
      headers: [],
    };
  },
  methods: {
    beforeUpload(file) {
      this.handleFileUpload(file);
      return false; // Prevent automatic upload
    },
    async handleFileUpload(file) {
      try {
        const data = await this.readFileAsync(file);
        const workbook = XLSX.read(data, { type: 'array' });
        const firstSheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[firstSheetName];
        const jsonSheet = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

        // 获取表头
        this.headers = jsonSheet[0] || [];
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    },
    readFileAsync(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = (error) => reject(error);
        reader.readAsArrayBuffer(file);
      });
    },
  },
};
</script>

<style scoped>
.excel-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.excel-table th, .excel-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.excel-table th {
  background-color: #f4f4f4;
}
</style>
