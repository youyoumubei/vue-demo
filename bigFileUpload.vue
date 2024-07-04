self.onmessage = function(event) {
  const file = event.data;
  const reader = new FileReader();

  reader.onload = function(e) {
    const data = new Uint8Array(e.target.result);
    postMessage(data);
  };

  reader.onerror = function(error) {
    postMessage({ error: error.message });
  };

  reader.readAsArrayBuffer(file);
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
      const worker = new Worker(new URL('../workers/fileReaderWorker.js', import.meta.url));
      worker.postMessage(file);

      worker.onmessage = (e) => {
        if (e.data.error) {
          console.error(e.data.error);
          return;
        }
        const data = e.data;
        const workbook = XLSX.read(data, { type: 'array' });
        const firstSheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[firstSheetName];
        const jsonSheet = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

        // 获取表头
        this.headers = jsonSheet[0] || [];
        worker.terminate();
      };

      worker.onerror = (error) => {
        console.error(error.message);
        worker.terminate();
      };

      // Prevent upload
      return false;
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
