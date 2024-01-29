export const CarType = Object.freeze({
  compact: "compact",
  medium: "medium",
  fullSize: "full-size",
  class1Truck: "class 1 truck",
  class2Truck: "class 2 truck",
});

export function getCarTypeByString(str) {
  const entry = Object.entries(CarType).find(([key, value]) => value === str);
  return entry ? CarType[entry[0]] : undefined;
}

const car_colors = Object.freeze({
  [CarType.compact]: "#d6ef84",
  [CarType.medium]: "#fbee8a",
  [CarType.fullSize]: "#ef957f",
  [CarType.class1Truck]: "#edbe94",
  [CarType.class2Truck]: "#6576c6",
});

const car_prices = Object.freeze({
  [CarType.compact]: 150,
  [CarType.medium]: 150,
  [CarType.fullSize]: 150,
  [CarType.class1Truck]: 250,
  [CarType.class2Truck]: 700,
});

const car_images = Object.freeze({
  [CarType.compact]: "/images/compact.png",
  [CarType.medium]: "/images/medium.png",
  [CarType.fullSize]: "/images/full_size.png",
  [CarType.class1Truck]: "/images/class1truck.png",
  [CarType.class2Truck]: "/images/class2truck.png",
});

export class Car {
  constructor(type) {
    this.type = type;
    this.price = car_prices[type];
    this.color = car_colors[type];
    this.image = car_images[type];
  }
}
