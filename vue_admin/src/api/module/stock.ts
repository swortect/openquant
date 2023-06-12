import Http from '../http';

export const getStockDaily = function(form: any) {
    return Http.get('/v1/stock/get_data/get_stock_daily', form.value)
}
export const setStockDaily = function(form: any) {
    return Http.get('/v1/stock/get_data/set_stock_daily', form.value)
}
export const getStockDetail = function(form: any) {
    return Http.get('/v1/stock/get_data/get_stock_detail', form)
}

export const setMfiRank = function(form: any) {
    return Http.get('/v1/stock/get_data/set_mfi_rank', form.value)
}
export const getMfiRank = function(form: any) {
    return Http.get('/v1/stock/get_data/get_mfi_rank', form.value)
}
