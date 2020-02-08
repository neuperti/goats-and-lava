import time


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
            self.draw_queue = Queue(is_response_queue=True)
            self.time_queue = Queue(is_response_queue=True)

    def get(self, wait_for_content=True, remaining_thinking_time=None):
        if remaining_thinking_time:
            end_time = time.time() + remaining_thinking_time
        if wait_for_content:
            while not self:
                if remaining_thinking_time:
                    if time.time() > end_time:
                        self.time_queue.append(end_time - time.time())
                        return "failed!"
                    else:
                        self.time_queue.append(end_time - time.time())
        else:
            if not self:
                return None
        return self.pop(0)

    def append(self, *new_command, wait_for_response=True):
        try:
            new_command = " ".join(new_command)
        except:
            new_command = new_command[0]
        list.append(self, new_command)
        if wait_for_response and not self.is_response_queue:
            return self.response_queue.get()
