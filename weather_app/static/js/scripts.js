/**
 * Funcion encargada de limitar el numero de opciones visibles en el datalist y de dar priridad a las palabras con la misma letra inicial
 */
var search = document.querySelector('#city');
        var results = document.querySelector('#listprod');
        var templateContent = document.querySelector('#listtemplate').content;
        search.addEventListener('keyup', function handler(event) {
            while (results.children.length) results.removeChild(results.firstChild);
            var inputVal = new RegExp(search.value.trim(), 'i');
            const firstChar = search.value.trim()[0];
            var set = Array.prototype.reduce.call(templateContent.cloneNode(true).children, function searchFilter(frag, item, i) {
                if (inputVal.test(item.value) && frag.children.length < 5 && firstChar.toLowerCase() == item.value[0].toLowerCase() ) frag.appendChild(item);
                return frag;
            }, document.createDocumentFragment());
            results.appendChild(set);
        });