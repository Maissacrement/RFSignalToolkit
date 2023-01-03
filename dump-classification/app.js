#!/bin/env node

// Fast dump type identification 
// With this algorithm you can fastly sorted best time shifting match 

const datastruct = {
  datagrams: [],
  moreThan: [],
  minusThan: [],
}

const typeDef = { moreThan: '+', minusThan: '-' }

const dataset = [ 5, 6, 8, 95, 5, 6, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ,11]

const train = (set) => set.forEach(data => model(data) ? datastruct.moreThan.push(data) : datastruct.minusThan.push(data))

const model = (number) => number > 6

const training = (numb) => {
  const num = parseInt(numb)
  // Trainning Model
  train(dataset)
  if (![].concat(datastruct['moreThan'], datastruct['minusThan']).includes(num)) train([num])

  Object.keys(datastruct).forEach(type => datastruct[type].map(x => x === num).filter(x => x).length ? console.log(typeDef[type], 'num:', num) : null )
}

const main = process.argv.slice(2, process.argv.length)

main.forEach(arg => training(arg))