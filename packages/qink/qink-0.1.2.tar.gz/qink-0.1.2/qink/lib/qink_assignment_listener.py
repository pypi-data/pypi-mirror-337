import abc


class QinkAssignmentListener(abc.ABC):

    @abc.abstractmethod
    def on_partitions_revoked(self, revoked: list[int]):
        """Called when partitions are revoked from this consumer.

        Args:
            revoked: List of partition IDs that were revoked
        """

    @abc.abstractmethod
    def on_partitions_assigned(self, assigned: list[int]):
        """Called when partitions are assigned to this consumer.

        Args:
            assigned: List of partition IDs that were assigned
        """
