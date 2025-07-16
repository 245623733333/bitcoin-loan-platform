import Array "mo:base/Array";

actor {
  type User = {
    name: Text;
    btcBalance: Nat;
    loan: Nat;
  };

  stable var users: [User] = [];

  public func registerUser(name: Text): async Text {
    let exists = Array.filter<User>(users, func(u: User): Bool {
      u.name == name
    });

    if (exists.size() > 0) {
      return "User already registered.";
    };

    let newUser: User = {
      name = name;
      btcBalance = 0;
      loan = 0;
    };

    users := Array.append(users, [newUser]);
    return "User registered: " # name;
  };

  public func getAllUsers(): async [User] {
    return users;
  };

  public func getUser(name: Text): async ?User {
    for (user in users.vals()) {
      if (user.name == name) {
        return ?user;
      };
    };
    return null;
  };

  public func deleteUser(name: Text): async Text {
    let filtered = Array.filter<User>(users, func(u: User): Bool {
      u.name != name
    });

    if (filtered.size() == users.size()) {
      return "User not found.";
    };

    users := filtered;
    return "User deleted: " # name;
  };

  public func depositBTC(name: Text, amount: Nat): async Text {
    var updatedUsers: [User] = [];
    var found: Bool = false;

    for (user in users.vals()) {
      if (user.name == name) {
        let updatedUser: User = {
          name = user.name;
          btcBalance = user.btcBalance + amount;
          loan = user.loan;
        };
        updatedUsers := Array.append(updatedUsers, [updatedUser]);
        found := true;
      } else {
        updatedUsers := Array.append(updatedUsers, [user]);
      };
    };

    if (not found) {
      return "User not found.";
    };

    users := updatedUsers;
    return "Deposited " # debug_show(amount) # " BTC to " # name;
  };

  public func repayLoan(name: Text, amount: Nat): async Text {
    var updatedUsers: [User] = [];
    var repaid: Bool = false;

    for (user in users.vals()) {
      if (user.name == name) {
        if (user.loan == 0) {
          return "No loan to repay.";
        } else if (user.btcBalance < amount) {
          return "Insufficient BTC balance.";
        };

        let repayAmount = if (amount > user.loan) user.loan else amount;

        updatedUsers := Array.append(updatedUsers, [{
          name = user.name;
          btcBalance = user.btcBalance - repayAmount;
          loan = user.loan - repayAmount;
        }]);

        repaid := true;
      } else {
        updatedUsers := Array.append(updatedUsers, [user]);
      };
    };

    if (not repaid) {
      return "User not found.";
    };

    users := updatedUsers;
    return "Loan repayment successful for " # name;
  };

  public func takeLoan(name: Text, amount: Nat): async Text {
    var updatedUsers: [User] = [];
    var found: Bool = false;

    for (user in users.vals()) {
      if (user.name == name) {
        let updatedUser: User = {
          name = user.name;
          btcBalance = user.btcBalance;
          loan = user.loan + amount;
        };
        updatedUsers := Array.append(updatedUsers, [updatedUser]);
        found := true;
      } else {
        updatedUsers := Array.append(updatedUsers, [user]);
      };
    };

    if (not found) {
      return "User not found.";
    };

    users := updatedUsers;
    return "Loan of " # debug_show(amount) # " granted to " # name;
  };
}
