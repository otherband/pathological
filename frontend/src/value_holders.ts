class ValueHolder<T> {

    value: T;

    constructor(value: T) {
        this.value = value;
    }

    getValue(): T {
        return this.value;
    }

    setValue(newValue: T) {
        this.value = newValue;
    }

}

const holder = new ValueHolder(15);
