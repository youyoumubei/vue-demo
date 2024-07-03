<template>
  <div>
    <a-upload :before-upload="beforeUpload" :show-upload-list="false">
      <a-button icon="upload">Click to Upload</a-button>
    </a-upload>
    <table v-if="sheetData.length" class="excel-table">
      <thead>
        <tr>
          <th v-for="(header, index) in sheetData[0]" :key="index">{{ header }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, rowIndex) in sheetData.slice(1)" :key="rowIndex">
          <td v-for="(cell, cellIndex) in row" :key="cellIndex">{{ cell }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import * as XLSX from 'xlsx';

export default {
  data() {
    return {
      sheetData: [],
    };
  },
  methods: {
    beforeUpload(file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: 'array' });
        const firstSheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[firstSheetName];
        const jsonSheet = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
        this.sheetData = jsonSheet;
      };
      reader.readAsArrayBuffer(file);
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
