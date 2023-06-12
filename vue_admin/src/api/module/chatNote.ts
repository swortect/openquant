import Http from '../http';

export const getHistoryList = function(form: any) {
    return Http.get('/v1/chat_note/history/index', form.value)
}
export const postHistory = function(form: any) {
    console.log(11111111)
    console.log(form)
    return Http.post('/v1/chat_note/history/post', form,{
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
}
export const saveHistory = function(form: any) {
  console.log(11111111)
  console.log(form)
  return Http.post('/v1/chat_note/history/save', form,{
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
}
export const deleteHistory = function(form: any) {
    return Http.post('/v1/chat_note/history/delete', form,{
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
}
export const getHistoryDetail = function(form: any) {
    return Http.get('/v1/chat_note/history/detail', form)
}
