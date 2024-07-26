<template>
  <div>
    <div v-for="(item, index) in dataList" :key="index" class="item-row">
      <a-input
        v-model="item.key"
        placeholder="Key"
        style="width: 40%; margin-right: 10px"
      />
      <a-input
        v-model="item.value"
        placeholder="Value"
        style="width: 40%; margin-right: 10px"
      />
      <a-button type="danger" @click="removeItem(index)">
        删除
      </a-button>
    </div>
    <a-button type="primary" @click="addItem">
      增加
    </a-button>
  </div>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  data() {
    return {
      dataList: [
        { key: '', value: '' },
        { key: '', value: '' }
      ]
    };
  },
  methods: {
    addItem() {
      this.dataList.push({ key: '', value: '' });
    },
    removeItem(index) {
      this.dataList.splice(index, 1);
    }
  }
});
</script>

<style scoped>
.item-row {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}
</style>
