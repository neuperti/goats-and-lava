
class Queue(list):
    """A queue. queue.append(x) loads command x in the queue and returns the response to the
    command. This will take until the response is loaded into the queue from the other side.
    The response is loaded into the queue using queue.response_queue.append(response). The
    response should be either True or False, depending on weather the command failed or not."""
    def __init__(self, is_response_queue=False):
        list.__init__(self)
        self.is_response_queue = is_response_queue
        if not is_response_queue:
            self.response_queue = Queue(is_response_queue=True)
            self.print_queue = Queue(is_response_queue=True)

    def get(self, wait_for_content=True):
        if wait_for_content:
            while not self:
                pass
        else:
            if not self:
                return None
        return self.pop(0)

    def append(self, *new_command):
        new_command = " ".join(new_command)
        list.append(self, new_command)
        if not self.is_response_queue:
            return self.response_queue.get()
