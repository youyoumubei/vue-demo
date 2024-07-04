uploadFileInChunks(file) {
      const CHUNK_SIZE = 2 * 1024 * 1024; // 2MB per chunk
      const totalChunks = Math.ceil(file.size / CHUNK_SIZE);
      let currentChunk = 0;

      const readChunk = () => {
        const start = currentChunk * CHUNK_SIZE;
        const end = Math.min(file.size, start + CHUNK_SIZE);
        const chunk = file.slice(start, end);
        const reader = new FileReader();

        reader.onload = (e) => {
          // Process chunk data
          const data = new Uint8Array(e.target.result);
          if (currentChunk === 0) {
            const workbook = XLSX.read(data, { type: 'array' });
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
    }
