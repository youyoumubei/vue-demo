const pairwiseGroup = (array) => {
  if (array.length % 2 !== 0) {
    throw new Error('Array length must be even');
  }

  return array.reduce((result, value, index, array) => {
    if (index % 2 === 0) {
      result.push(array.slice(index, index + 2));
    }
    return result;
  }, []);
};

const compareData = (array, key) => {
  const groups = pairwiseGroup(array);
  const identical = [];
  const sourceOnlyNull = [];
  const targetOnlyNull = [];
  const different = [];

  groups.forEach(([source, target]) => {
    const sourceValue = source[key];
    const targetValue = target[key];

    if (sourceValue === targetValue) {
      identical.push(source, target);
    } else if (sourceValue === null && targetValue !== null) {
      sourceOnlyNull.push(source, target);
    } else if (sourceValue !== null && targetValue === null) {
      targetOnlyNull.push(source, target);
    } else {
      different.push(source, target);
    }
  });

  return { identical, sourceOnlyNull, targetOnlyNull, different };
};

const result = compareData(arr, 'name');
console.log('Identical:', result.identical);
console.log('Source Only Null:', result.sourceOnlyNull);
console.log('Target Only Null:', result.targetOnlyNull);
console.log('Different:', result.different);
