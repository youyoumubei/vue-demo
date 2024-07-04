<template>
  <div>
    <a-upload :before-upload="beforeUpload" :show-upload-list="false">
      <a-button icon="upload">Click to Upload</a-button>
    </a-upload>
    <a-progress :percent="uploadProgress" status="active" v-if="uploadProgress > 0 && uploadProgress < 100" />
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
      uploadProgress: 0,
    };
  },
  methods: {
    beforeUpload(file) {
      this.uploadFileInChunks(file);
      return false; // Prevent automatic upload
    },
    uploadFileInChunks(file) {
      const CHUNK_SIZE = 2 * 1024 * 1024; // 2MB per chunk
      const totalChunks = Math.ceil(file.size / CHUNK_SIZE);
      let currentChunk = 0;
      let workbook = null;

      const readChunk = () => {
        const start = currentChunk * CHUNK_SIZE;
        const end = Math.min(file.size, start + CHUNK_SIZE);
        const chunk = file.slice(start, end);
        const reader = new FileReader();

        reader.onload = (e) => {
          // Process chunk data
          const data = new Uint8Array(e.target.result);
          if (currentChunk === 0) {
            // Read only the first chunk to get headers
            workbook = XLSX.read(data, { type: 'array' });
            const firstSheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[firstSheetName];
            const jsonSheet = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

            // 获取表头
            this.headers = jsonSheet[0] || [];
          }

          currentChunk++;
          this.uploadProgress = (currentChunk / totalChunks) * 100;

          if (currentChunk < totalChunks) {
            readChunk();
          }
        };

        reader.onerror = (error) => {
          console.error('Error reading chunk:', error);
        };

        reader.readAsArrayBuffer(chunk);
      };

      readChunk();
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
