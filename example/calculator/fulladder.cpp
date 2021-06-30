/*
 * Parent SST model
 *
 * */

#include <sst/core/component.h>
#include <sst/core/interfaces/stringEvent.h>
#include <sst/core/link.h>

class FullAdder : public SST::Component {
public:
    FullAdder(SST::ComponentId_t, SST::Params&);

    void setup() override;

    void finish() override;

    void handle_opand1(SST::Event*);

    void handle_opand2(SST::Event*);

    void handle_cin(SST::Event*);

    bool tick(SST::Cycle_t);

    // Register the component
    SST_ELI_REGISTER_COMPONENT(FullAdder, // class
                               "calculator", // element library
                               "fulladder", // component
                               SST_ELI_ELEMENT_VERSION(1, 0, 0),
                               "SST parent model",
                               COMPONENT_CATEGORY_UNCATEGORIZED)

    // Port name, description, event type
    SST_ELI_DOCUMENT_PORTS({"opand1", "Operand 1", {"sst.Interfaces.StringEvent"}},
                           {"opand2", "Operand 2", {"sst.Interfaces.StringEvent"}},
                           {"cin", "Carry-in", {"sst.Interfaces.StringEvent"}},
                           {"sum", "Sum", {"sst.Interfaces.StringEvent"}},
                           {"cout", "Carry-out", {"sst.Interfaces.StringEvent"}})

private:
    // SST parameters
    std::string clock;

    // SST links
    SST::Link *opand1_link, *opand2_link, *cin_link, *sum_link, *cout_link;

    // other attributes
    std::string opand1, opand2, cin;
    SST::Output output;
};

FullAdder::FullAdder(SST::ComponentId_t id, SST::Params& params)
    : SST::Component(id), clock(params.find<std::string>("clock", "")), opand1(""), opand2(""),
      cin("") {

    opand1_link = configureLink(
        "opand1", new SST::Event::Handler<FullAdder>(this, &FullAdder::handle_opand1));
    opand2_link = configureLink(
        "opand2", new SST::Event::Handler<FullAdder>(this, &FullAdder::handle_opand2));
    cin_link =
        configureLink("cin", new SST::Event::Handler<FullAdder>(this, &FullAdder::handle_cin));
    sum_link = configureLink("sum");
    cout_link = configureLink("cout");

    output.init("\033[34m" + getName() + "\033[0m -> ", 1, 0, SST::Output::STDOUT);

    if (!(opand1_link && opand2_link && sum_link && cout_link)) {
        output.fatal(CALL_INFO, -1, "Failed to configure port\n");
    }

    registerClock(clock, new SST::Clock::Handler<FullAdder>(this, &FullAdder::tick));
}

void FullAdder::setup() {
    output.verbose(CALL_INFO, 1, 0, "Component is being set up.\n");
}

void FullAdder::finish() {
    output.verbose(CALL_INFO, 1, 0, "Destroying %s...\n", getName().c_str());
}

void FullAdder::handle_opand1(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        opand1 = se->getString();
    }
    delete ev;
}

void FullAdder::handle_opand2(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        opand2 = se->getString();
    }
    delete ev;
}

void FullAdder::handle_cin(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        cin = se->getString();
    }
    delete ev;
}

bool FullAdder::tick(SST::Cycle_t current_cycle) {

    if (current_cycle) {
        bool opand1_bit = (opand1 == "1");
        bool opand2_bit = (opand2 == "1");
        bool cin_bit = (cin == "1");

        bool sum_bit = ((opand1_bit ^ opand2_bit) ^ cin_bit);
        bool cout_bit = ((opand1_bit & opand2_bit) | (cin_bit & (opand1_bit ^ opand2_bit)));

        sum_link->send(new SST::Interfaces::StringEvent(sum_bit ? "1" : "0"));
        cout_link->send(new SST::Interfaces::StringEvent(cout_bit ? "1" : "0"));
    }
    return false;
}
