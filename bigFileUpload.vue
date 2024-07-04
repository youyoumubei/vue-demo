uploadFileInChunks(file) {
      const CHUNK_SIZE = 512 * 1024; // 512KB per chunk
      let offset = 0;
      let chunkIndex = 0;
      const totalChunks = Math.ceil(file.size / CHUNK_SIZE);

      const readChunk = () => {
        const reader = new FileReader();
        const chunk = file.slice(offset, offset + CHUNK_SIZE);

        reader.onload = (e) => {
          const data = new Uint8Array(e.target.result);
          const workbook = XLSX.read(data, { type: 'array' });
          const firstSheetName = workbook.SheetNames[0];
          const worksheet = workbook.Sheets[firstSheetName];
          const jsonSheet = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

          if (chunkIndex === 0) {
            // Read headers only for the first chunk
            this.headers = jsonSheet[0] || [];
          }

          offset += CHUNK_SIZE;
          chunkIndex++;
          this.uploadProgress = (offset / file.size) * 100;

          if (offset < file.size) {
            readChunk();
          }
        };

        reader.onerror = (error) => {
          console.error('Error reading chunk:', error);
        };

        reader.readAsArrayBuffer(chunk);
      };

      readChunk();
    }
