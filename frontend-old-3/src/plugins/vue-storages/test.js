updateArray(key, data, using = 'id') {
  if (!using) {
    throw new Error('updateArray needs a key to identify the dictionnries to update')
  }
  const result = this.retrieve(key)
  if (result) {
    const existingIds = result.map(x => x[using])
    const incomingIds = data.map(x => x[using])
    const indexesToUpdate = []
    const nonExistingIndexes = []
    incomingIds.forEach((incomingId, i) => {
      existingIds.forEach((existingId) => {
        if (incomingId === existingId) {
          indexesToUpdate.push(i)
        } else {
          nonExistingIndexes.push(i)
        }
      })
    })

    indexesToUpdate.forEach((index) => {
      result[index] = data[index]
    })

    nonExistingIndexes.forEach((index) => {
      result.push(data[index])
    })
  }
}
