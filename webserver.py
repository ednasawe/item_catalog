from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD Operations from Lesson 1
from database_setup import Base, Book, BookItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create a session that connects to the books database
engine = create_engine('sqlite:///bookitem.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # Creating a new book category page
            if self.path.endswith("/books/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Add a New Book Category</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/books/new'>"
                output += "<input name = 'newBookName' type = 'text' placeholder = 'Add a new book here' > "
                output += "<input type='submit' value='ADD'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return


            if self.path.endswith("/edit"):
                bookIDPath = self.path.split("/")[2]
                myBookQuery = session.query(Book).filter_by(
                    id=bookIDPath).one()
                if myBookQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myBookQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/books/%s/edit' >" % bookIDPath
                    output += "<input name = 'newBookName' type='text' placeholder = '%s' >" % myBookQuery.name
                    output += "<input type = 'submit' value = 'Rename'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)

            
            if self.path.endswith("/delete"):
                bookIDPath = self.path.split("/")[2]

                myBookQuery = session.query(Book).filter_by(
                    id=bookIDPath).one()
                if myBookQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to delete %s?" % myBookQuery.name
                    output += "<form method='POST' enctype = 'multipart/form-data' action = '/books/%s/delete'>" % bookIDPath
                    output += "<input type = 'submit' value = 'Delete'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)

            # Creating the book page
            if self.path.endswith("/books"):
                books = session.query(Book).all()
                output = ""
                # Creating a function that is used to
                # create a new book item category
                output += "<a href = '/books/new' > ADD A NEW BOOK HERE </a></br></br>"
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += "<html><body>"
                for book in books:
                    output += book.name
                    output += "</br>"
                    # Creating the edit and delete functions for
                    # adding and removieng the books items
                    output += "<a href ='/books/%s/edit' >Edit </a> "% book.id
                    output += "</br>"
                    output += "<a href =' /books/%s/delete'> Delete </a>"% book.id
                    output += "</br></br></br>"

                output += "</body></html>"
                self.wfile.write(output)
                return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    # Creating a post request function to allows user to
    # create and add new book category and books
    def do_POST(self):
        try:
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newBookName')
                    bookIDPath = self.path.split("/")[2]

                    myBookQuery = session.query(Book).filter_by(
                        id=bookIDPath).one()
                    if myBookQuery != []:
                        myBookQuery.name = messagecontent[0]
                        session.add(myBookQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/books')
                        self.end_headers() 


            if self.path.endswith("/delete"):
                bookIDPath = self.path.split("/")[2]
                myBookQuery = session.query(Book).filter_by(
                    id=bookIDPath).one()
                if myBookQuery:
                    session.delete(myBookQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/books')
                    self.end_headers()

            if self.path.endswith("/books/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newBookName')

                    # Creating a new Book category Item
                    newBook = Book(name=messagecontent[0])
                    session.add(newBook)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/books')
                    self.end_headers()

        except:
            pass


def main():
    try:
        server = HTTPServer(('', 5000), webServerHandler)
        print ('Web server in now running...open localhost:5000/books in your browser')
        server.serve_forever()
    except KeyboardInterrupt:
        print ('^C received, shutting down server')
        server.socket.close()

if __name__ == '__main__':
    main()