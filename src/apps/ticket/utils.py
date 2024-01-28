

# Set ticket's files upload path
def ticket_file_src(instance, path):
    ticket_id = instance.ticket.id
    return f'files/tickets/{ticket_id}/{path}'
