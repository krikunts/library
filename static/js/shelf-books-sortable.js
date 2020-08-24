$(function () {
    doAjaxSetup();
    const list = $('ul.sortable').sortable({
        onDrop: function (item, container, _super) {
            const data = list.sortable("serialize").get();
            const json = JSON.stringify(data);
            _super(item, container);
            $.ajax({
                type: "POST",
                contentType: "application/json",
                data: json,
                url: window.location.href,
                complete: function (resp) {
                    if (resp.responseJSON.status === "success") {
                        showMessage("success", "Изменения сохранены");
                    } else {
                        showMessage("danger", resp.responseJSON.error || "Ошибка");
                        let elems = [];
                        for (let i = 0; i < resp.responseJSON.books.length; i++) {
                            elems.push($("li[data-book=" + resp.responseJSON.books[i] + "]").clone());
                        }
                        list.empty().append(elems);
                    }
                }
            });
        }
    });
});