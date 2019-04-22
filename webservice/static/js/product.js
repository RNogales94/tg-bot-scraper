
class Product {
    constructor(obj){
        this.shortDescription = obj.shortDescription;
        this.description = obj.description;
        this.features = obj.features;
        this.standardPrice = obj.standardPrice;
        this.price = obj.price;
        this.size = obj.size;
        this.url = obj.url;
        this.imageUrl = obj.imageUrl;
    }

    toHTML(){
        return `<div class="column is-narrow">
                <article class="card" style="width: 340px">
                    <header class="card-header">
                        <p class="card-header-title">
                            <a title="Ver en Amazon" href=${this.url}>${this.shortDescription}</a>
                        </p>
                    </header>
                    <div class="card-image">
                        <figure class="image">
                            <img src="${this.imageUrl}" alt="${this.description + this.features}">
                        </figure>
                    </div>
                    <footer class="card-footer">
                        <div class="tags">
                          <span class="tag is-danger">Antes: ${this.standardPrice}</span>
                          <span class="tag is-success">Ahora: ${this.price}</span>
                        </div>
                        <div name="rater"></div>
                    </footer>
                </article>
            </div>`
    }
    toElement(){
        return htmlToElement(this.toHTML())
    }
}