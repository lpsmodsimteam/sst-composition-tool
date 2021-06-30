/*
 * Parent SST model
 *
 * */

#include <sst/core/component.h>
#include <sst/core/interfaces/stringEvent.h>
#include <sst/core/link.h>

class RippleCarryAdder : public SST::Component {
public:
    RippleCarryAdder(SST::ComponentId_t, SST::Params&);

    void setup() override;

    void finish() override;

    void handle_as_opand1_0(SST::Event*);

    void handle_as_opand1_1(SST::Event*);

    void handle_as_opand1_2(SST::Event*);

    void handle_as_opand1_3(SST::Event*);

    void handle_as_opand2_0(SST::Event*);

    void handle_as_opand2_1(SST::Event*);

    void handle_as_opand2_2(SST::Event*);

    void handle_as_opand2_3(SST::Event*);

    void handle_as_cin_0(SST::Event*);

    void handle_add_sum_0(SST::Event*);

    void handle_add_sum_1(SST::Event*);

    void handle_add_sum_2(SST::Event*);

    void handle_add_sum_3(SST::Event*);

    void handle_add_cout_0(SST::Event*);

    void handle_add_cout_1(SST::Event*);

    void handle_add_cout_2(SST::Event*);

    void handle_add_cout_3(SST::Event*);

    bool tick(SST::Cycle_t);

    // Register the component
    SST_ELI_REGISTER_COMPONENT(RippleCarryAdder, // class
                               "calculator", // element library
                               "ripplecarryadder", // component
                               SST_ELI_ELEMENT_VERSION(1, 0, 0),
                               "SST parent model",
                               COMPONENT_CATEGORY_UNCATEGORIZED)

    // Port name, description, event type
    SST_ELI_DOCUMENT_PORTS(
        // adder-subtractor ports
        {"as_opand1_0", "Operand 1 (0) of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},
        {"as_opand1_1", "Operand 1 (1) of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},
        {"as_opand1_2", "Operand 1 (2) of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},
        {"as_opand1_3", "Operand 1 (3) of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},

        {"as_opand2_0", "Operand 2 (0) of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},
        {"as_opand2_1", "Operand 2 (1) of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},
        {"as_opand2_2", "Operand 2 (2) of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},
        {"as_opand2_3", "Operand 2 (3) of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},

        {"as_cin_0", "Carry-in of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},

        {"as_sum_0", "Sum (0) of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},
        {"as_sum_1", "Sum (1) of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},
        {"as_sum_2", "Sum (2) of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},
        {"as_sum_3", "Sum (3) of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},

        {"as_cout_3", "Operand 1 of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},

        // full adder ports
        // full adder 0
        {"add_opand1_0", "Operand 1 of Full Adder 0", {"sst.Interfaces.StringEvent"}},
        {"add_opand2_0", "Operand 2 of Full Adder 0", {"sst.Interfaces.StringEvent"}},
        {"add_cin_0", "Carry-in of Full Adder 0", {"sst.Interfaces.StringEvent"}},
        {"add_sum_0", "Sum of Full Adder 0", {"sst.Interfaces.StringEvent"}},
        {"add_cout_0", "Carry-out of Full Adder 0", {"sst.Interfaces.StringEvent"}},

        // full adder 1
        {"add_opand1_1", "Operand 1 of Full Adder 1", {"sst.Interfaces.StringEvent"}},
        {"add_opand2_1", "Operand 2 of Full Adder 1", {"sst.Interfaces.StringEvent"}},
        {"add_cin_1", "Carry-in of Full Adder 1", {"sst.Interfaces.StringEvent"}},
        {"add_sum_1", "Sum of Full Adder 1", {"sst.Interfaces.StringEvent"}},
        {"add_cout_1", "Carry-out of Full Adder 1", {"sst.Interfaces.StringEvent"}},

        // full adder 2
        {"add_opand1_2", "Operand 1 of Full Adder 2", {"sst.Interfaces.StringEvent"}},
        {"add_opand2_2", "Operand 2 of Full Adder 2", {"sst.Interfaces.StringEvent"}},
        {"add_cin_2", "Carry-in of Full Adder 2", {"sst.Interfaces.StringEvent"}},
        {"add_sum_2", "Sum of Full Adder 2", {"sst.Interfaces.StringEvent"}},
        {"add_cout_2", "Carry-out of Full Adder 2", {"sst.Interfaces.StringEvent"}},

        // full adder 3
        {"add_opand1_3", "Operand 1 of Full Adder 3", {"sst.Interfaces.StringEvent"}},
        {"add_opand2_3", "Operand 2 of Full Adder 3", {"sst.Interfaces.StringEvent"}},
        {"add_cin_3", "Carry-in of Full Adder 3", {"sst.Interfaces.StringEvent"}},
        {"add_sum_3", "Sum of Full Adder 3", {"sst.Interfaces.StringEvent"}},
        {"add_cout_3", "Carry-out of Full Adder 3", {"sst.Interfaces.StringEvent"}}, )

private:
    // SST parameters
    std::string clock;

    // SST links
    SST::Link *as_cin_0_link, *as_cout_3_link, *as_opand1_links[4], *as_opand2_links[4],
        *as_sum_links[4], *add_opand1_links[4], *add_opand2_links[4], *add_cin_links[4],
        *add_sum_links[4], *add_cout_links[4];

    // other attributes
    int num_bits;
    std::string opand1[4], opand2[4], cin[4], sum[4], cout[4];
    SST::Output output;
};

RippleCarryAdder::RippleCarryAdder(SST::ComponentId_t id, SST::Params& params)
    : SST::Component(id), clock(params.find<std::string>("clock", "")),
      num_bits(4), opand1{"X", "X", "X", "X"}, opand2{"X", "X", "X", "X"}, cin{"X", "X", "X", "X"},
      sum{"X", "X", "X", "X"}, cout{"X", "X", "X", "X"} {

    add_opand1_links[0] = configureLink("add_opand1_0");
    add_opand1_links[1] = configureLink("add_opand1_1");
    add_opand1_links[2] = configureLink("add_opand1_2");
    add_opand1_links[3] = configureLink("add_opand1_3");

    add_opand2_links[0] = configureLink("add_opand2_0");
    add_opand2_links[1] = configureLink("add_opand2_1");
    add_opand2_links[2] = configureLink("add_opand2_2");
    add_opand2_links[3] = configureLink("add_opand2_3");

    add_cin_links[0] = configureLink("add_cin_0");
    add_cin_links[1] = configureLink("add_cin_1");
    add_cin_links[2] = configureLink("add_cin_2");
    add_cin_links[3] = configureLink("add_cin_3");

    as_sum_links[0] = configureLink("as_sum_0");
    as_sum_links[1] = configureLink("as_sum_1");
    as_sum_links[2] = configureLink("as_sum_2");
    as_sum_links[3] = configureLink("as_sum_3");

    as_cout_3_link = configureLink("as_cout_3");

    as_opand1_links[0] = configureLink(
        "as_opand1_0",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_as_opand1_0));
    as_opand1_links[1] = configureLink(
        "as_opand1_1",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_as_opand1_1));
    as_opand1_links[2] = configureLink(
        "as_opand1_2",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_as_opand1_2));
    as_opand1_links[3] = configureLink(
        "as_opand1_3",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_as_opand1_3));

    as_opand2_links[0] = configureLink(
        "as_opand2_0",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_as_opand2_0));
    as_opand2_links[1] = configureLink(
        "as_opand2_1",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_as_opand2_1));
    as_opand2_links[2] = configureLink(
        "as_opand2_2",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_as_opand2_2));
    as_opand2_links[3] = configureLink(
        "as_opand2_3",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_as_opand2_3));

    as_cin_0_link = configureLink(
        "as_cin_0",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_as_cin_0));

    add_sum_links[0] = configureLink(
        "add_sum_0",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_add_sum_0));
    add_sum_links[1] = configureLink(
        "add_sum_1",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_add_sum_1));
    add_sum_links[2] = configureLink(
        "add_sum_2",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_add_sum_2));
    add_sum_links[3] = configureLink(
        "add_sum_3",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_add_sum_3));

    add_cout_links[0] = configureLink(
        "add_cout_0",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_add_cout_0));
    add_cout_links[1] = configureLink(
        "add_cout_1",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_add_cout_1));
    add_cout_links[2] = configureLink(
        "add_cout_2",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_add_cout_2));
    add_cout_links[3] = configureLink(
        "add_cout_3",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_add_cout_3));

    output.init("\033[34mparent-" + getName() + "\033[0m -> ", 1, 0, SST::Output::STDOUT);

    if (!as_cin_0_link) {
        output.fatal(CALL_INFO, -1, "Failed to configure port\n");
    }
    if (!as_cout_3_link) {
        output.fatal(CALL_INFO, -1, "Failed to configure port\n");
    }
    for (int i = 0; i < num_bits; i++) {
        if (!as_opand1_links[i]) {
            output.fatal(CALL_INFO, -1, "Failed to configure port\n");
        }
    }
    for (int i = 0; i < num_bits; i++) {
        if (!as_opand2_links[i]) {
            output.fatal(CALL_INFO, -1, "Failed to configure port\n");
        }
    }
    for (int i = 0; i < num_bits; i++) {
        if (!as_sum_links[i]) {
            output.fatal(CALL_INFO, -1, "Failed to configure port\n");
        }
    }

    for (int i = 0; i < num_bits; i++) {
        if (!add_opand1_links[i]) {
            output.fatal(CALL_INFO, -1, "Failed to configure port\n");
        }
    }
    for (int i = 0; i < num_bits; i++) {
        if (!add_opand2_links[i]) {
            output.fatal(CALL_INFO, -1, "Failed to configure port\n");
        }
    }
    for (int i = 0; i < num_bits; i++) {
        if (!add_cin_links[i]) {
            output.fatal(CALL_INFO, -1, "Failed to configure port\n");
        }
    }

    for (int i = 0; i < num_bits; i++) {
        if (!add_sum_links[i]) {
            output.fatal(CALL_INFO, -1, "Failed to configure port\n");
        }
    }
    for (int i = 0; i < num_bits; i++) {
        if (!add_cout_links[i]) {
            output.fatal(CALL_INFO, -1, "Failed to configure port\n");
        }
    }

    registerClock(clock, new SST::Clock::Handler<RippleCarryAdder>(this, &RippleCarryAdder::tick));

    // Tell SST to wait until we authorize it to exit
    registerAsPrimaryComponent();
    primaryComponentDoNotEndSim();
}

void RippleCarryAdder::setup() {
    output.verbose(CALL_INFO, 1, 0, "Component is being set up.\n");
}

void RippleCarryAdder::finish() {
    output.verbose(CALL_INFO, 1, 0, "Destroying %s...\n", getName().c_str());
    std::cout << "OPAND1: ";
    for (int i = 3; i > -1; i--) {
        std::cout << opand1[i];
    }

    std::cout << "\nOPAND2: ";
    for (int i = 3; i > -1; i--) {
        std::cout << opand2[i];
    }

    std::cout << "\nCIN:    ";
    for (int i = 3; i > -1; i--) {
        std::cout << cin[i];
    }

    std::cout << "\nSUM:    ";
    for (int i = 3; i > -1; i--) {
        std::cout << sum[i];
    }

    std::cout << "\nCOUT:   ";
    for (int i = 3; i > -1; i--) {
        std::cout << cout[i];
    }
    std::cout << '\n';
}

void RippleCarryAdder::handle_as_cin_0(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        cin[0] = se->getString();
        add_cin_links[0]->send(new SST::Interfaces::StringEvent(cin[0]));
    }
    delete ev;
}

void RippleCarryAdder::handle_as_opand1_0(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        opand1[0] = se->getString();
        add_opand1_links[0]->send(new SST::Interfaces::StringEvent(opand1[0]));
    }
    delete ev;
}

void RippleCarryAdder::handle_as_opand2_0(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        opand2[0] = se->getString();
        add_opand2_links[0]->send(new SST::Interfaces::StringEvent(opand2[0]));
    }
    delete ev;
}

void RippleCarryAdder::handle_add_cout_0(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        cout[0] = se->getString();
        add_cin_links[1]->send(new SST::Interfaces::StringEvent(cout[0]));
    }
    delete ev;
}

void RippleCarryAdder::handle_add_sum_0(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        sum[0] = se->getString();
        as_sum_links[0]->send(new SST::Interfaces::StringEvent(sum[0]));
    }
    delete ev;
}

void RippleCarryAdder::handle_as_opand1_1(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        opand1[1] = se->getString();
        add_opand1_links[1]->send(new SST::Interfaces::StringEvent(opand1[1]));
    }
    delete ev;
}

void RippleCarryAdder::handle_as_opand2_1(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        opand2[1] = se->getString();
        add_opand2_links[1]->send(new SST::Interfaces::StringEvent(opand2[1]));
    }
    delete ev;
}

void RippleCarryAdder::handle_add_cout_1(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        cout[1] = se->getString();
        cin[1] = cout[0];
        add_cin_links[2]->send(new SST::Interfaces::StringEvent(cout[1]));
    }
    delete ev;
}

void RippleCarryAdder::handle_add_sum_1(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        sum[1] = se->getString();
        as_sum_links[1]->send(new SST::Interfaces::StringEvent(sum[1]));
    }
    delete ev;
}

void RippleCarryAdder::handle_as_opand1_2(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        opand1[2] = se->getString();
        add_opand1_links[2]->send(new SST::Interfaces::StringEvent(opand1[2]));
    }
    delete ev;
}

void RippleCarryAdder::handle_as_opand2_2(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        opand2[2] = se->getString();
        add_opand2_links[2]->send(new SST::Interfaces::StringEvent(opand2[2]));
    }
    delete ev;
}

void RippleCarryAdder::handle_add_cout_2(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        cout[2] = se->getString();
        cin[2] = cout[1];
        add_cin_links[3]->send(new SST::Interfaces::StringEvent(cout[2]));
    }
    delete ev;
}

void RippleCarryAdder::handle_add_sum_2(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        sum[2] = se->getString();
        as_sum_links[2]->send(new SST::Interfaces::StringEvent(sum[2]));
    }
    delete ev;
}

void RippleCarryAdder::handle_as_opand1_3(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        opand1[3] = se->getString();
        add_opand1_links[3]->send(new SST::Interfaces::StringEvent(opand1[3]));
    }
    delete ev;
}

void RippleCarryAdder::handle_as_opand2_3(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        opand2[3] = se->getString();
        add_opand2_links[3]->send(new SST::Interfaces::StringEvent(opand2[3]));
    }
    delete ev;
}

void RippleCarryAdder::handle_add_cout_3(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        cout[3] = se->getString();
        cin[3] = cout[2];
        as_cout_3_link->send(new SST::Interfaces::StringEvent(cout[3]));
    }
    delete ev;
}

void RippleCarryAdder::handle_add_sum_3(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        sum[3] = se->getString();
        as_sum_links[3]->send(new SST::Interfaces::StringEvent(sum[3]));
    }
    delete ev;
}

bool RippleCarryAdder::tick(SST::Cycle_t) {

    return false;
}
