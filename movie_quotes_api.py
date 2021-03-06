
import endpoints
import protorpc

from models import MovieQuote
import main

@endpoints.api(name="moviequotes", version="v1", description="Movie QUotes API")
class MovieQuotesApi(protorpc.remote.Service):
    pass

    #Methods returns a single object or query methods return a collection
    @MovieQuote.method(name="moviequote.insert", path="moviequote/insert", http_method="POST")
    def moviequote_insert(self, request):
        """ insert or update a quote """
        if request.from_datastore:
            my_quote = request
        else:
            my_quote = MovieQuote(parent=main.PARENT_KEY, quote=request.quote, movie=request.movie)
        my_quote.put()
        #one way to get parent key
        #request.put()
        #no parent key here
        return request
    
    @MovieQuote.query_method(query_fields = ("limit", "order", "pageToken"),
                             name="moviequote.list",
                             path="moviequote/list",
                             http_method="GET")
    def moviequote_list(self, query):
        """ get all quotes """
        return query
    
    @MovieQuote.method(request_fields = ("entityKey",),
                       name="moviequote.delete",
                       path="moviequote/delete/{entityKey}",
                       http_method="DELETE")
    def moviequote_delete(self, request):
        """ delete a quote if it is there """
        if not request.from_datastore:
            raise endpoints.NotFoundException("movie quote to be deleted not found")
        request.key.delete()
        return MovieQuote(quote="deleted")
    
app = endpoints.api_server([MovieQuotesApi], restricted = False)